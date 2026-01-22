import pytest
from utils.assert_helper import SoftAssert, assert_list_sorted
from utils.cv_helper import CVHelper
from utils.notify_helper import NotifyHelper

def test_soft_assert():
    """Verify SoftAssert collects errors and only fails at the end."""
    sa = SoftAssert()
    sa.expect_true(True, "Should pass")
    sa.expect_true(False, "Should fail 1")
    sa.expect_equal(1, 2, "Should fail 2")
    
    with pytest.raises(AssertionError) as excinfo:
        sa.assert_all()
    
    assert "Soft Assert failed with 2 errors" in str(excinfo.value)

def test_assert_helpers():
    """Verify standalone assert helpers."""
    data = [1, 2, 3]
    assert_list_sorted(data)
    
    with pytest.raises(AssertionError):
        assert_list_sorted([3, 2, 1])

def test_notify_structure():
    """Verify NotifyHelper generates correct payloads."""
    summary = {"total": 10, "passed": 8, "failed": 2}
    
    # Test Lark
    lark_payload = NotifyHelper._format_lark_card(summary)
    assert lark_payload['msg_type'] == 'interactive'
    assert lark_payload['card']['header']['template'] == 'red'  # failed > 0

    # Test DingTalk
    ding_payload = NotifyHelper._format_dingtalk_md(summary)
    assert ding_payload['msgtype'] == 'markdown'
    assert "- **Failed**: 2" in ding_payload['markdown']['text']

def test_cv_helper_imports():
    """Verify CVHelper can import cv2."""
    try:
        import cv2
        assert cv2.__version__ is not None
    except ImportError:
        pytest.skip("opencv-python not installed")
