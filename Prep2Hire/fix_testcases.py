"""
Run with: python fix_testcases.py
This script shows all test cases and fixes empty ones for known problems.
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prep2Hire.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from judge.models import Problem, TestCase

print("\n=== Current Test Cases ===")
for prob in Problem.objects.all():
    print(f"\nProblem: {prob.title} (slug={prob.slug})")
    tcs = prob.testcases.all()
    if not tcs.exists():
        print("  (no test cases)")
    for tc in tcs:
        print(f"  TC {tc.id}: input={repr(tc.input_data[:60])} | expected={repr(tc.expected_output[:60])}")

# ── Fix empty test cases for "Sum of Two Numbers" ──
print("\n=== Fixing empty test cases ===")

SUM_FIXES = [
    {"input_data": "2\n3",    "expected_output": "Sum: 5"},
    {"input_data": "10\n20",  "expected_output": "Sum: 30"},
    {"input_data": "100\n200","expected_output": "Sum: 300"},
]

try:
    prob = Problem.objects.get(slug="sum-of-two-numbers")
    tcs  = list(prob.testcases.all())
    for i, fix in enumerate(SUM_FIXES):
        if i < len(tcs):
            tc = tcs[i]
            if not tc.input_data.strip() or not tc.expected_output.strip():
                tc.input_data      = fix["input_data"]
                tc.expected_output = fix["expected_output"]
                tc.save()
                print(f"  Fixed TC {tc.id}: input={repr(tc.input_data)} → expected={repr(tc.expected_output)}")
            else:
                print(f"  TC {tc.id} already has data, skipping.")
        else:
            # Create missing test case
            tc = TestCase.objects.create(
                problem=prob,
                input_data=fix["input_data"],
                expected_output=fix["expected_output"]
            )
            print(f"  Created TC {tc.id}: input={repr(tc.input_data)} → expected={repr(tc.expected_output)}")
    print("\n✅ Done! Now go to /coding/problem/sum-of-two-numbers/submit/ and re-submit.")
except Problem.DoesNotExist:
    print("  Problem 'sum-of-two-numbers' not found. Listing all slugs:")
    for p in Problem.objects.all():
        print(f"    {p.slug}")
    print("\nEdit fix_testcases.py and update the slug + expected outputs to match your problem.")
