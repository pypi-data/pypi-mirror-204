from pydantic import BaseModel


class TaxPredictParam(BaseModel):
    """
    税收分类识别服务 参数模型
    """
    # 序列化
    sn: str = None
    # 输入文本
    text: str = None


class InfoExtractParam(BaseModel):
    """
    信息抽取服务,商品分类服务 参数模型
    """
    # 序列化
    sn: str = None
    # 输入文本
    text: str = None
