#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Checklist """

# standard python imports

from dataclasses import dataclass
from typing import Any

from app.api import Api
from app.application import Application
from app.logz import create_logger

logger = create_logger()


@dataclass
class Checklist:
    """RegScale Checklist

    :return: RegScale Checklist
    """

    # Required
    status: str
    assetId: int
    tool: str
    baseline: str

    id: int = 0
    isPublic: bool = True
    uuid: str = None
    vulnerabilityId: str = None
    ruleId: str = None
    cci: str = None
    check: str = None
    results: str = None
    comments: str = None
    createdById: str = None
    dateCreated: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None

    def __hash__(self):
        """
        Enable object to be hashable
        :return: Hashed Checklist
        """
        return hash(
            (
                self.baseline,
                self.check,
                self.assetId,
                self.cci,
                self.ruleId,
                self.vulnerabilityId,
            )
        )

    @staticmethod
    def get_checklists(
        parent_id: int, parent_module: str = "components"
    ) -> list["Checklist"]:
        """Return all checklists for a given component
        :param parent_id: RegScale parent id
        :param component_id: RegScale component id
        :return: _description_
        """
        app = Application()
        api = Api(app)
        logger.info("Fetching all checklists for component %s", parent_id)
        checklists = []
        query = """
                           query {
                securityChecklists(skip: 0, take: 50,where:{asset: {parentId: {eq: parent_id_placeholder}, parentModule: {eq: "parent_module_placeholder"}}}) {
                    items {
                            id
                            asset {
                              id
                              name
                              parentId
                              parentModule
                            }
                            status
                            tool
                            vulnerabilityId
                            ruleId
                            cci
                            check
                            results
                            baseline
                            comments
                    }
                    totalCount
                    pageInfo {
                        hasNextPage
                    }
                }
            }
            """.replace(
            "parent_id_placeholder", str(parent_id)
        ).replace(
            "parent_module_placeholder", parent_module
        )
        data = api.graph(query)
        if "securityChecklists" in data and "items" in data["securityChecklists"]:
            for item in data["securityChecklists"]["items"]:
                item["assetId"] = item["asset"]["id"]
                checklists.append(item)
        return checklists

    @staticmethod
    def from_dict(obj: Any) -> "Checklist":
        _id = int(obj.get("id", 0))
        _isPublic = bool(obj.get("isPublic"))
        _uuid = str(obj.get("uuid"))
        _tool = str(obj.get("tool"))
        _vulnerabilityId = str(obj.get("vulnerabilityId"))
        _ruleId = str(obj.get("ruleId"))
        _cci = str(obj.get("cci"))
        _baseline = str(obj.get("baseline"))
        _check = str(obj.get("check"))
        _results = str(obj.get("results"))
        _comments = str(obj.get("comments"))
        _status = str(obj.get("status"))
        _assetId = int(obj.get("assetId", 0))
        _createdById = str(obj.get("createdById"))
        _dateCreated = str(obj.get("dateCreated"))
        _lastUpdatedById = str(obj.get("lastUpdatedById"))
        # _dateLastUpdated = str(obj.get("dateLastUpdated"))
        return Checklist(
            _status,
            _assetId,
            _tool,
            _baseline,
            _id,
            _isPublic,
            _uuid,
            _vulnerabilityId,
            _ruleId,
            _cci,
            _check,
            _results,
            _comments,
            _createdById,
            _dateCreated,
            _lastUpdatedById,
        )
