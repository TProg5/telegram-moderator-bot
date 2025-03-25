add_warn = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a> 
    <b>receives a warning for: {$reason}.</b>\n
    <b><i>Number of warnings: {$warns}.</i></b>\n
    <b>Admin: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)

finally_warn = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a> 
    <b>is muted for 30 minutes due to exceeding the warning limit.</b>\n
    <b>Admin: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)
