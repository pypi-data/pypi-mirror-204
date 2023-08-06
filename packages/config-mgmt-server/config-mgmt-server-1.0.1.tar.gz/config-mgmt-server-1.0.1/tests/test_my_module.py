# -*- coding: utf-8 -*-

from __future__ import annotations
import config_mgmt_server    # The code to test


class TestSrc:
    def test_build(self) -> None:
        assert config_mgmt_server.main() == "test"
