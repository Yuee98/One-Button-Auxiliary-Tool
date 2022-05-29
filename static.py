from tools import check, js

action_path = check('js/actions.js')
context = js(action_path).eval()

actions = context.actions
base = context.base
special = context.special
buff = context.changeWithBuff

job_filter_id = {
    '骑士': 262144,
    '战士': 1048576,
    '暗黑骑士': 2147483648,
    '绝枪战士': 68719476736,

    '白魔法师': 8388608,
    '学者': 134217728,
    '占星师': 4294967296,
    '贤者': 549755813888,

    '忍者': 536870912,
    '武僧': 524288,
    '武士': 8589934592,
    '龙骑士': 2097152,
    '钐镰客': 274877906944,

    '诗人': 4194304,
    '机工士': 1073741824,
    '舞者': 137438953472,

    '黑魔法师': 16777216,
    '召唤师': 67108864,
    '赤魔法师': 17179869184,
}