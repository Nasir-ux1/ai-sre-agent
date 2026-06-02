import os
import sys
from ai_sre.tools import SRETools

def test_check_disk():
    res = SRETools.check_disk()
    assert "status" in res
    assert res["status"] in ["success", "error"]

def test_check_services():
    res = SRETools.check_services("nginx")
    assert "status" in res
    assert res["status"] in ["success", "error"]

def test_check_network():
    res = SRETools.check_network(80)
    assert "status" in res
    assert "is_blocked" in res or res["status"] == "error"

def test_check_processes():
    res = SRETools.check_processes()
    assert "status" in res
    assert "output" in res or res["status"] == "error"

def test_check_logs():
    res = SRETools.check_logs("error", 5)
    assert "status" in res
    assert "output" in res or res["status"] == "error"