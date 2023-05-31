import logging
import math
import time
import glm
import threading

from raid_helper import utils as raid_utils
from raid_helper.data import special_actions
from raid_helper.utils.typing import *

# special_actions[9913] = raid_utils.fan_shape(23)  # 披萨饼
special_actions[9913] = 0
special_actions[9914] = 0  # 奈尔百万核爆
special_actions[9949] = 0  # 百万核爆大圈
special_actions[9930] = 0  # 死宣白圈
special_actions[9951] = 0  # 百万核爆塔
special_actions[9942] = 0  # 十亿核爆
special_actions[9905] = 0  # 以太失控
# special_actions[9968] = 0  # 百京核爆
# special_actions[9964] = 0  # 无尽顿悟
Ucob = raid_utils.MapTrigger(733)

center = glm.vec3(100, 0, 100)

logger = logging.getLogger('raid_helper/Ucob')


def _draw_disperse(actor: raid_utils.NActor, range, dura):
    normal_surface = glm.vec4(.6, 1, .6, .2)
    danger_surface = glm.vec4(1, .6, .6, .2)
    normal_line = glm.vec4(.2, 1, .2, .7)
    danger_line = glm.vec4(1, .2, .2, .7)

    def get_surface(omen: raid_utils.BaseOmen):
        return danger_surface if any(
            omen.is_hit(a.pos)
            for a in raid_utils.iter_main_party(exclude_id=actor.update().id)
        ) else normal_surface

    def get_line(omen: raid_utils.BaseOmen):
        return danger_line if any(
            omen.is_hit(a.pos)
            for a in raid_utils.iter_main_party(exclude_id=actor.update().id)
        ) else normal_line

    return raid_utils.draw_circle(radius=range, pos=actor, duration=dura, surface_color=get_surface,
                                  line_color=get_line)


class Timer:
    last_run_time = 0


@Ucob.on_npc_yell(6493, 6492, 6494, 6496, 6495, 6497, 6500, 6501, 6502, 6503, 6504, 6505, 6506, 6507)
def on_npc_yell(evt: NetworkMessage[zone_server.NpcYell]):
    now = time.time()
    if now - Timer.last_run_time < 2:
        return
    Timer.last_run_time = now

    actor = raid_utils.NActor.by_id(evt.message.actor_id)
    match evt.message.npc_yell_id:
        case 6493:  # 月光啊！用你的炽热烧尽敌人！
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
        case 6492:  # 月光啊！照亮铁血霸道！
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
            raid_utils.sleep(5)
            raid_utils.draw_circle(radius=10, pos=actor, duration=4)
        case 6494:  # 被炽热灼烧过的轨迹，乃成铁血霸道！
            raid_utils.sleep(5)
            raid_utils.draw_circle(radius=10, pos=actor, duration=4)
        case 6496:  # 我降临于此，征战铁血霸道！
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=5)
            raid_utils.sleep(5)
            raid_utils.draw_circle(radius=10, pos=actor, duration=4)
        case 6495:  # 炽热燃烧！给予我月亮的祝福！
            raid_utils.sleep(5)
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
        case 6497:  # 我降临于此，对月长啸！
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=5)
            raid_utils.sleep(5)
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
        case 6500:  # 超新星啊，更加闪耀吧！在星降之夜，称赞红月！
            yichou = raid_utils.NActor.by_id(actor.target_id)
            raid_utils.sleep(10)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=4, dura=5)
            raid_utils.sleep(5)
            raid_utils.draw_circle(radius=4, pos=yichou, duration=3)
        case 6501:  # 超新星啊，更加闪耀吧！照亮红月下炽热之地！
            yichou = raid_utils.NActor.by_id(actor.target_id)
            raid_utils.sleep(10)
            raid_utils.draw_circle(radius=4, pos=yichou, duration=5)
        case 6502:  # 我降临于此对月长啸！召唤星降之夜！
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=5)
            raid_utils.sleep(5)
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
            raid_utils.sleep(5)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=4, dura=5)
        case 6503:  # 我自月而来降临于此，召唤星降之夜！
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
            raid_utils.sleep(5)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=5)
            raid_utils.sleep(5)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=4, dura=5)
        case 6504:  # 钢铁燃烧吧！成为我降临于此的刀剑吧！
            raid_utils.draw_circle(radius=10, pos=actor, duration=4)
            raid_utils.sleep(10)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=4)
        case 6505:  # 钢铁成为我降临于此的燃烧之剑！
            raid_utils.draw_circle(radius=10, pos=actor, duration=4)
            raid_utils.sleep(5)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=4)
        case 6506:  # 我自月而来降临于此，踏过炽热之地！
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
            raid_utils.sleep(5)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=4)
        case 6507:  # 我自月而来携钢铁降临于此！
            raid_utils.draw_circle(inner_radius=6, radius=22, pos=actor, duration=5)
            raid_utils.sleep(5)
            raid_utils.draw_circle(radius=10, pos=actor, duration=4)
            raid_utils.sleep(5)
            for a in raid_utils.iter_main_party():
                _draw_disperse(a, range=3, dura=4)


@Ucob.on_add_status(466)
def on_add_status_light(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    # 雷点名
    actor = raid_utils.NActor.by_id(evt.source_id)
    if raid_utils.assert_status(actor, evt.param.status_id, 5):
        raid_utils.draw_circle(radius=5, pos=actor, duration=4)


@Ucob.on_lockon(40)
def on_lockon_earth_shake(msg: ActorControlMessage[actor_control.SetLockOn]):
    # 大地摇动
    normal_surface = glm.vec4(.6, 1, .6, .2)
    danger_surface = glm.vec4(1, .6, .6, .2)
    normal_line = glm.vec4(.2, 1, .2, .7)
    danger_line = glm.vec4(1, .2, .2, .7)
    bahamut = next(raid_utils.find_actor_by_base_id(0x1FE8))
    t_actor = raid_utils.NActor.by_id(msg.source_id)

    def get_surface(omen: raid_utils.BaseOmen):
        return danger_surface if any(
            omen.is_hit(a.pos)
            for a in raid_utils.iter_main_party(exclude_id=t_actor.update().id)
        ) else normal_surface

    def get_line(omen: raid_utils.BaseOmen):
        return danger_line if any(
            omen.is_hit(a.pos)
            for a in raid_utils.iter_main_party(exclude_id=t_actor.update().id)
        ) else normal_line

    raid_utils.draw_fan(pos=bahamut, facing=lambda _: glm.polar(t_actor.update().pos - bahamut.update().pos).y,
                        radius=30, degree=90, duration=6, surface_color=get_surface, line_color=get_line)


@Ucob.on_cast(9955)
def on_cast_nael(evt: 'NetworkMessage[zone_server.ActorCast]'):
    # 一秒找奈尔
    nael = next(raid_utils.find_actor_by_base_id(0x1FE1))
    me = raid_utils.main.mem.actor_table.me
    raid_utils.sleep(5)
    raid_utils.draw_line(me, nael, duration=8, color=glm.vec4(.2, 1, .2, .7), width=5)


@Ucob.on_cast(9959)
def on_cast_bahamut(evt: 'NetworkMessage[zone_server.ActorCast]'):
    # 一秒找巴哈对面
    bahamut = next(raid_utils.find_actor_by_base_id(0x1FE8))
    me = raid_utils.main.mem.actor_table.me
    raid_utils.sleep(5)
    raid_utils.draw_rect(
        length=50, width=4, pos=bahamut,
        facing=lambda _: glm.polar(me.pos - bahamut.pos).y,
        duration=5,
    )


@Ucob.on_cast(9968)
def on_cast_exaflare(evt: 'NetworkMessage[zone_server.ActorCast]'):
    # 百京核爆
    fac = evt.message.facing
    pos = evt.message.pos
    x = evt.message.pos.x
    y = evt.message.pos.y
    z = evt.message.pos.z
    raid_utils.draw_circle(pos=glm.vec3(pos.x, pos.y, pos.z), radius=6, duration=3.7)
    raid_utils.sleep(3.7)
    for i in range(1, 6):
        x += math.sin(fac) * 8
        z += math.cos(fac) * 8
        raid_utils.draw_circle(pos=glm.vec3(x, y, z), radius=6, duration=1.5)
        raid_utils.sleep(1.5)