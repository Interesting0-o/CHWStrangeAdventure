from Pages.Page import Page

class PagesGroup:
    def __init__(self):
        """
        添加页面到PagesGroup
        """
        self.pages:list[Page] = []
        self.is_init = False

    def __len__(self)->int:
        """
        获取页面数量
        :return:
        """
        return len(self.pages)

    def add_page(self,*pages:Page):
        """
        添加页面
        :param pages
        :return:
        """
        for p in pages:
            try:
                self.pages.append(p)
            except Exception as e:
                print(f"添加页面{p.path}失败：{e}")
                exit()

    def insert_page(self, index:int, page:Page):
        """
        插入页面
        :param index:
        :param page:
        :return:
        """
        self.pages.insert(index, page)
    def remove_page(self, page:Page):
        """
        移除页面
        :param page:
        :return:
        """
        self.pages.remove(page)

    def get_page(self, index:int)->Page:
        """
        获取页面
        :param index:
        :return:
        """
        return self.pages[index]

    def get_pages(self)->list:
        """
        获取所有页面
        :return:
        """
        return self.pages

    def pages_init(self)->None:
        """
        初始化所有页面
        :return:
        """
        for page in self.pages:
            page.init()
        self.is_init = True

    def handle_event(self, event)->None:
        """
        处理事件
        :param event:
        :return:
        """
        for page in self.pages:
            page.handle_event(event)

    def reset(self)->None:
        """
        重置所有页面
        :return:
        """
        for page in self.pages:
            page.reset()

    def is_pages_init(self)->bool:
        """
        判断是否所有页面都初始化
        :return:
        """
        return self.is_init

    def change_page_end(self)->None:
        """
        切换页面结束
        :return:
        """
        for page in self.pages:
            page.is_end = True
