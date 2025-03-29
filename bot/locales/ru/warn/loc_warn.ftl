add_warn = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a> 
    <b>получает предупреждение по причине: {$reason}.</b>\n
    <b><i>Количество предупреждений: {$warns}.</i></b>\n
    <b>Админ: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)

finally_warn = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a> 
    <b>получает мут на 30 минут из-за превышения количества предпреждений.</b>\n
    <b>Админ: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)