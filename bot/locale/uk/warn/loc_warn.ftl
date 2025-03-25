add_warn = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a>
    <b>отримує попередження, причина: {$reason}.</b>\n
    <b><i>Кількість попередженнь: {$warns}.</i></b>\n
    <b>Адмін: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)

finally_warn = (
    👀<a href='tg://user?id={$user_id}'><b>{$user_full_name}</b></a> 
    <b>отримує мут на 30 хвилин через превіщення кількості попередженнь.</b>\n
    <b>Адмін: <a href='tg://user?id={$admin_id}'><b>{$admin_full_name}</b></a>
)