#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.api import Api
from app.application import Application
from app.commercial.stig import STIG, cci_control_mapping


class Test_Stig:
    """Test STIG Integrations"""

    def test_stig(self):
        """Run STIG integration and make sure it works"""
        app = Application()
        api = Api(app)
        config = app.config
        ssp_id = 371
        # Get all plan implementations and set to fail
        for imp in api.get(
            url=f"{config['domain']}/api/controlImplementation/getAllByPlan/{ssp_id}"
        ).json():
            imp["status"] = "Not Implemented"
            api.put(
                url=f"{config['domain']}/api/controlImplementation/{imp['id']}",
                json=imp,
            )
        mapping = cci_control_mapping(force=False)
        STIG(
            folder_path="./tests/test_data", regscale_ssp_id=ssp_id, cci_mapping=mapping
        )
        updated_imps = api.get(
            url=f"{config['domain']}/api/controlImplementation/getAllByPlan/{ssp_id}"
        ).json()
        # IA-7 should be fully implemented
        assert [imp["status"] for imp in updated_imps if imp["controlName"] == "ia-7"][
            0
        ] == "Fully Implemented"
