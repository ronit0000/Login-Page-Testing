"""
Pytest configuration and hooks
"""
import pytest
import os
from datetime import datetime


def pytest_configure(config):
    """Create report directories if they don't exist"""
    report_dir = "reports"
    screenshot_dir = "screenshots"
    
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the PyTest Plugin to take and embed screenshots in HTML report
    whenever a test fails.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Store the result for use in fixtures
    setattr(item, f"rep_{report.when}", report)
    
    if report.when == "call":
        # Log test result
        if report.failed:
            print(f"\n❌ FAILED: {item.nodeid}")
        elif report.passed:
            print(f"\n✅ PASSED: {item.nodeid}")
        elif report.skipped:
            print(f"\n⏭️  SKIPPED: {item.nodeid}")


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Login Page Test Results"


def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom summary to HTML report"""
    prefix.extend([
        "<h2>Test Execution Summary</h2>",
        f"<p>Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        "<p>Testing the Login Page for boundary values, functional requirements, "
        "security vulnerabilities, and performance metrics.</p>",
        "<hr>"
    ])


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their names"""
    for item in items:
        # Auto-add markers based on test names
        if "email" in item.nodeid.lower():
            item.add_marker(pytest.mark.email)
        if "password" in item.nodeid.lower():
            item.add_marker(pytest.mark.password)
        if "sql" in item.nodeid.lower():
            item.add_marker(pytest.mark.sql_injection)
        if "xss" in item.nodeid.lower():
            item.add_marker(pytest.mark.xss)


@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    """Setup that runs once per test session"""
    print("\n" + "=" * 70)
    print("🚀 Starting Login Page Test Suite")
    print("=" * 70)
    
    yield
    
    print("\n" + "=" * 70)
    print("✅ Test Suite Completed")
    print("=" * 70)


@pytest.fixture(scope="function", autouse=True)
def test_wrapper(request):
    """Wrapper for each test"""
    test_name = request.node.name
    print(f"\n{'─' * 70}")
    print(f"🧪 Running: {test_name}")
    print(f"{'─' * 70}")
    
    yield
    
    # Test cleanup if needed
