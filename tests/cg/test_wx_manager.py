from cg.wx_manager import WxManager

def test_manager_label():
    m = WxManager('data/go')
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')
