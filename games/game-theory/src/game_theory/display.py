"""Local Chinese labels; never included in API observations."""
NAMES={'prisoner-dilemma':'囚徒困境','stag-hunt':'猎鹿博弈','hawk-dove':'鹰鸽博弈','public-goods':'公共物品','ultimatum':'最后通牒'}
TAGLINES={'prisoner-dilemma':'各自选择合作或背叛，再一起揭示。','stag-hunt':'共同猎鹿，或独自选择稳妥的猎兔。','hawk-dove':'面对同一份资源，选择强硬或退让。','public-goods':'把本轮所得投入公共池，或保留给自己。','ultimatum':'一方提出分配，另一方决定是否接受。'}
RULES_ZH={
 'prisoner-dilemma':'双方同时选择合作或背叛。双方合作各得 3；单方背叛时，背叛方得 5、合作方得 0；双方背叛各得 1。',
 'stag-hunt':'双方同时选择猎鹿或猎兔。共同猎鹿各得 4；独自猎鹿得 0；猎兔固定得 3。',
 'hawk-dove':'双方同时选择退让或强硬。双方退让各得 2；单方强硬时，强硬方得 4、退让方得 0；双方强硬各得 −1。',
 'public-goods':'每人每轮获得 10，选择全部贡献或全部保留。公共池乘以 1.6，再由所有参与者均分。个人本轮收益等于保留部分加上公共池分配；没有跨轮财富约束。',
 'ultimatum':'每轮分配 10。提议方给对方 0、2、5、8 或 10；接受后按报价分配，拒绝则双方得 0。P1 在奇数轮提议，P2 在偶数轮提议。'}
STRATEGY_ZH={'jev':'Jev 模型','cooperate':'始终合作','defect':'始终强硬','random':'均匀随机','cycle':'循环','tit_for_tat':'针锋相对','generous':'宽容互惠','win_stay_lose_shift':'赢留输换'}
ACTION_ZH={'cooperate':'合作','defect':'背叛','stag':'猎鹿','hare':'猎兔','dove':'退让','hawk':'强硬','contribute':'贡献 10','keep':'保留 10','accept':'接受','reject':'拒绝',**{'offer_'+str(x):'给对方 '+str(x) for x in (0,2,5,8,10)}}
VARIANTS={'base':'基础条件','history-0':'历史窗口 0','history-5':'历史窗口 5','unknown-horizon':'不告知总轮数','random-stop':'随机终止','execution-noise':'5% 执行翻转','one-intervention':'第 10 轮干预 P1'}
STATUS={'complete':'完整','paused':'暂停／失败','incomplete':'未完成','dependency_blocked':'接口依赖阻塞'}

def strategy_definitions(s):
    if s=='ultimatum':
        return {
         'jev':'调用固定版本真实 Jev，以最大化自己整场累计收益为目标。',
         'cooperate':'报价 5；接受给自己至少 5 的报价。',
         'defect':'报价 0；接受任何合法报价。',
         'random':'合法报价均匀随机；回应时等概率接受或拒绝。',
         'cycle':'报价按 0／10 轮换，接受阈值按 0／5 轮换；分别按自己担任该角色的次数与起始相位推进。',
         'tit_for_tat':'报价复制对方最近一次实际报价，无历史时报 5；接受阈值为对方此前最近一次报价，无历史时为 5，不用本轮报价作为阈值。',
         'generous':'报价复制对方最近一次报价，无历史时报 5；接受阈值固定为 2，低于阈值仍以 0.25 概率接受。',
         'win_stay_lose_shift':'两个角色分别保存最近一次原始行动和收益。首次报价 5、首次回应接受；同角色上次收益至少 5 则保持，否则报价在 0／5 间切换、回应在接受／拒绝间切换。'}
    threshold={'prisoner-dilemma':3,'stag-hunt':3,'hawk-dove':2,'public-goods':10}[s]
    good,bad={'prisoner-dilemma':('合作','背叛'),'stag-hunt':('猎鹿','猎兔'),'hawk-dove':('退让','强硬'),'public-goods':('贡献全部 10','保留全部 10')}[s]
    return {
     'jev':'调用固定版本真实 Jev，以最大化自己整场累计收益为目标。',
     'cooperate':'每轮选择'+good+'。','defect':'每轮选择'+bad+'。',
     'random':'在两种合法行动间均匀随机，使用保存的独立随机种子。',
     'cycle':f'按 {good}／{bad} 交替，使用公开轮次和起始相位。',
     'tit_for_tat':f'首轮选择{good}；之后其他玩家上一轮至少一半执行合作类行动时选择{good}，否则选择{bad}。',
     'generous':f'同针锋相对；原本应选择{bad}时，以 0.25 概率改为{good}。',
     'win_stay_lose_shift':f'首轮选择{good}。自己上一轮实际收益至少为 {threshold} 时保持上一轮原始行动，否则切换。'}
