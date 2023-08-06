from pydantic import BaseModel


class TextParam(BaseModel):
    """
    税收分类识别服务 参数模型
    """
    # 序列化
    sn: str = None
    # 输入文本
    text: str = None
