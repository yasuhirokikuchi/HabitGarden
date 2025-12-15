# レベル・XP
def get_level_info(xp: int,LEVEL_DATA):
    
    # デフォルト値（レベル0）
    current_img = LEVEL_DATA[0]["image"]
    current_label = LEVEL_DATA[0]["label"]
    next_xp = 100 

    # 現在のレベルを判定
    for threshold, info in sorted(LEVEL_DATA.items()):
        if xp >= threshold:
            current_img = info["image"]
            current_label = info["label"]
        else:
            next_xp = threshold
            break
    
    # 最高レベルを超えている場合の処理（次の目標がない場合）
    max_threshold = max(LEVEL_DATA.keys())
    if xp >= max_threshold:
        next_xp = max_threshold # あるいはもっと大きな値

    # 進捗バーの計算
    prev_threshold = max([k for k in LEVEL_DATA.keys() if k <= xp], default=0)
    level_range = next_xp - prev_threshold
    progress_in_level = xp - prev_threshold

    if level_range > 0 and xp < max_threshold:
        progress_percent = min(1.0, max(0.0, progress_in_level / level_range))
    else:
        progress_percent = 1.0

    return current_img, current_label, progress_percent, next_xp
