import rule_engine
from .constants import NOT_SAME_TOWER_RULE

panelist_tower_context = rule_engine.Context(
    type_resolver=rule_engine.type_resolver_from_dict(
        {
            "sid": rule_engine.DataType.STRING,
            "name": rule_engine.DataType.STRING,
            "email": rule_engine.DataType.STRING,
            "lob": rule_engine.DataType.STRING,
            "is_available": rule_engine.DataType.BOOLEAN,
            "number_of_interviews...in_a_month": rule_engine.DataType.FLOAT,
            "prefered_round": rule_engine.DataType.STRING,
            "location": rule_engine.DataType.STRING,
        }
    )
)


def find_different_tower(candidate_tower, panelists_list):
    
    global NOT_SAME_TOWER_RULE

    NOT_SAME_TOWER_RULE = NOT_SAME_TOWER_RULE.format(candidate_tower)
    print(NOT_SAME_TOWER_RULE)
    not_same_tower_rule = rule_engine.Rule(NOT_SAME_TOWER_RULE, context=panelist_tower_context)

    matches_list = [not_same_tower_rule.matches({"lob":panelist['lob']}) for panelist in panelists_list]
                    
    return matches_list

