mute-user = 
    👀<b><a href='tg://user?id={ $user_id }'>{ $user_full_name }</a> is muted for { $measure_time }</b>
    <b>Reason: { $reason }</b>
    <b>Admin: <a href='tg://user?id={ $admin_id }'>{ $admin_full_name }</a></b>

ban-user =
    👀<b><a href='tg://user?id={$user_id}'>{$user_full_name}</a> is banned for {$measure_time}</b>
    <b>Reason: {$reason}</b>
    <b>Admin: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</a></b>