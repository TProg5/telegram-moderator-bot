mute-user = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a>
    <b>is muted for {$time} {$measure_time}</b>/n
    <b>Reason: {$reason}</b>\n
    <b>Admin: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)

ban-user = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a>
    <b>is banned for {$time} {$measure_time}</b>/n
    <b>Reason: {$reason}</b>\n
    <b>Admin: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)