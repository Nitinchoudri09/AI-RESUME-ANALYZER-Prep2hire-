from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Problem, Submission, TestCase
from .forms import SubmissionForm
from django.utils import timezone
import json, re
from .runner import run_python_code


# ── Helpers ──────────────────────────────────────────────────────────────────

def normalize_input(code, input_data):
    """
    Test cases often store values space-separated on one line (e.g. '2 3'),
    but code may call input() twice expecting two separate lines.
    This converts space-separated single-line input to one token per line.
    """
    n_inputs = len(re.findall(r'\binput\s*\(', code))
    if n_inputs <= 1:
        return input_data
    lines = [l for l in input_data.strip().split('\n') if l.strip()]
    if len(lines) >= n_inputs:
        return '\n'.join(lines)
    # fewer lines than input() calls → split by whitespace
    tokens = input_data.split()
    if len(tokens) >= n_inputs:
        return '\n'.join(tokens)
    return input_data


def clean_stdout(stdout, code):
    """
    Remove input() prompt strings from stdout so comparison only checks
    the real printed output, not the prompts the user added.
    e.g. 'Enter first number: Enter second number: Sum: 5' → 'Sum: 5'
    """
    prompts = re.findall(r'\binput\s*\(\s*["\']([^"\']*)["\']', code)
    result = stdout
    for p in prompts:
        result = result.replace(p, '')
    # collapse extra blank lines / spaces introduced by removal
    result = '\n'.join(l for l in result.splitlines() if l.strip())
    return result.strip()


# ── API: Run Code (AJAX) ──────────────────────────────────────────────────────

@csrf_exempt
def run_code(request):
    """
    POST { code, stdin }
    Returns JSON: { stdout, stderr, exit_code, time_taken }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    code  = body.get("code", "").strip()
    stdin = body.get("stdin", "")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    exit_code, stdout, stderr, time_taken = run_python_code(code, stdin)

    return JsonResponse({
        "stdout":     stdout,
        "stderr":     stderr,
        "exit_code":  exit_code,
        "time_taken": round(time_taken, 4),
        "error":      None,
    })


# ── Views ─────────────────────────────────────────────────────────────────────

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, "judge/problem_list.html", {"problems": problems})


def problem_detail(request, slug):
    prob = get_object_or_404(Problem, slug=slug)
    return render(request, "judge/problem_detail.html", {"problem": prob})


def submit_solution(request, slug):
    prob = get_object_or_404(Problem, slug=slug)
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            submission = Submission.objects.create(
                user=request.user if request.user.is_authenticated else None,
                problem=prob,
                code=code,
                status='RUNNING',
                created_at=timezone.now()
            )

            tcs = prob.testcases.all()
            results = []
            all_passed = True
            total_time = 0.0

            for tc in tcs:
                # Normalize input: convert "2 3" → "2\n3" if code calls input() twice
                normalized_input = normalize_input(code, tc.input_data)

                exit_code, stdout, stderr, t_taken = run_python_code(code, normalized_input)
                total_time += t_taken

                passed = False
                verdict = ""

                if exit_code is None:
                    verdict = "TLE"
                elif exit_code != 0:
                    verdict = f"Runtime Error"
                else:
                    # Strip prompt text before comparing
                    out_clean      = clean_stdout(stdout, code)
                    expected_clean = tc.expected_output.strip()
                    if out_clean == expected_clean:
                        verdict = "Accepted"
                        passed  = True
                    else:
                        verdict = f"Wrong Answer"

                results.append({
                    "tc_id":    tc.id,
                    "passed":   passed,
                    "verdict":  verdict,
                    "input":    normalized_input,
                    "output":   clean_stdout(stdout, code),
                    "expected": tc.expected_output.strip(),
                    "error":    stderr.strip() if stderr.strip() else "",
                    "time":     round(t_taken, 4),
                })
                if not passed:
                    all_passed = False

            submission.runtime = total_time
            submission.details = json.dumps(results, indent=2)
            submission.status  = 'AC' if all_passed else 'WA'
            submission.save()

            return redirect('judge:submission_result', submission_id=submission.id)
    else:
        form = SubmissionForm()
    return render(request, "judge/submit.html", {"problem": prob, "form": form})


def submission_result(request, submission_id):
    sub = get_object_or_404(Submission, pk=submission_id)
    details = []
    try:
        details = json.loads(sub.details)
    except Exception:
        details = [{"error": "No details available"}]
    return render(request, "judge/submission_result.html", {"submission": sub, "details": details})
