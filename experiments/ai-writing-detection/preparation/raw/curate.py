"""Keep short original essays and autobiographical prose; exclude catalog mislabels."""

import csv
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAOSHE = set("""
记涤洲|哭白涤洲|想北平|友来话北平|船上|生日|自谴|我所认识的沫若先生|敬悼许地山先生（二）|悼赵玉三司机师|成绩欠佳，收入更欠佳|可爱的成都|旧诗与贫血|四大皆空|一年之计在于春|在捷克斯洛伐克观剧|北京|反对文人无行|当作家并无捷径|悼念罗常培先生|北京干净|归自莫斯科|会外散记|眼福|天桥|南游杂感|下乡简记|更大一些的想象（济南通信）|济南的药集（济南通信）|广智院（济南通信）|观画记|小病|避暑|写字|读书|落花生|有钱最好|歇夏（也可以叫作“放青”）|青岛与我|我的理想家庭|搬家|大明湖之春|文艺与木匠|假若我有那么一箱子画|“住”的梦|在火车上|闲谈|猫
""".strip().split("|"))

XIAOHONG = set("""
魯迅先生生活散記|八月之日記一|失眠之夜|女子裝飾的心理|孤獨的生活|初冬|最後的一個星期|患病|又是冬天|劇團|冊子|春意掛上了樹梢|幾個歡快的日子|飛雪|搬家|夏夜|煩擾的一日|祖父死了的時候|長安寺|滑竿|牙粉醫病法|無題
""".strip().split("|"))

rows = list(csv.DictReader((HERE / "all_qualified.csv").open(encoding="utf-8-sig")))
selected = []
for row in rows:
    author, title = row["author"], row["title"]
    if author == "老舍" and title not in LAOSHE:
        continue
    if author == "萧红" and title not in XIAOHONG:
        continue
    if author == "许地山" or (author == "郁达夫" and title == "故事"):
        continue
    # The strict extraction pass has already excluded old/classical prose, prefaces,
    # translations, obvious fiction/drama and texts outside the length/block bounds.
    selected.append(row)

with (HERE / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(selected)
print("curated", len(selected), dict(Counter(row["author"] for row in selected)))
