"""Schema JSON pour POST /risk/calculate."""

risk_dto = {
    "type": "object",
    "properties": {
        "entreprise_id": {"type": "integer", "minimum": 1},
    },
    "required": ["entreprise_id"],
    "additionalProperties": False,
}