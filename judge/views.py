from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem, Submission, TestCase
from .forms import SubmissionForm
from django.utils import timezone
import json
from .runner import run_python_code

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, "judge/problem_list.html", {"problems": problems})

def problem_detail(request, slug):
    prob = get_object_or_404(Problem, slug=slug)
    return render(request, "judge/problem_detail.html", {"problem": prob})

def submit_solution(request, slug):
    prob = get_object_or_404(Problem, slug=slug)
    results = None
    total_time = 0.0
    all_passed = False
    submission_status = None
    submitted_code = None
    
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            submitted_code = code
            submission = Submission.objects.create(
                user=request.user if request.user.is_authenticated else None,
                problem=prob,
                code=code,
                status='RUNNING',
                created_at=timezone.now()
            )

            # Run against testcases synchronously (demo). Hide hidden TCs if desired.
            tcs = prob.testcases.all()
            results = []
            all_passed = True
            total_time = 0.0
            for tc in tcs:
                exit_code, stdout, stderr, t_taken = run_python_code(code, tc.input_data)
                total_time += t_taken
                passed = False
                verdict = ""
                if exit_code is None:
                    verdict = "TLE"
                    passed = False
                elif exit_code != 0:
                    verdict = f"RE: {stderr.strip()[:300]}"
                    passed = False
                else:
                    # Normalize whitespace to compare
                    out_clean = stdout.strip()
                    expected_clean = tc.expected_output.strip()
                    if out_clean == expected_clean:
                        verdict = "AC"
                        passed = True
                    else:
                        verdict = f"WA - expected {expected_clean!r} but got {out_clean!r}"
                        passed = False

                results.append({
                    "tc_id": tc.id,
                    "passed": passed,
                    "verdict": verdict,
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "stdout": stdout,
                    "stderr": stderr,
                    "time": t_taken
                })
                if not passed:
                    all_passed = False

            submission.runtime = total_time
            submission.details = json.dumps(results, indent=2)
            submission.status = 'AC' if all_passed else 'WA'
            submission.save()
            submission_status = submission.status
    else:
        form = SubmissionForm()
    
    return render(request, "judge/submit.html", {
        "problem": prob, 
        "form": form,
        "results": results,
        "total_time": total_time,
        "all_passed": all_passed,
        "submission_status": submission_status,
        "submitted_code": submitted_code
    })

def submission_result(request, submission_id):
    sub = get_object_or_404(Submission, pk=submission_id)
    details = []
    try:
        details = json.loads(sub.details)
    except Exception:
        details = [{"error": "No details"}]
    return render(request, "judge/submission_result.html", {"submission": sub, "details": details})
