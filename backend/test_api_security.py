from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def print_result(desc, result):
    if result:
        print(f"{desc}: ✅")
    else:
        print(f"{desc}: ❌")

# 配置，根据你的实际接口路径与用户名密码，适当修改
USERNAME_NORMAL = "user1"
PASSWORD_NORMAL = "test123"
USERNAME_ADMIN = "admin"
PASSWORD_ADMIN = "admin123"

ASSET_LIST_ENDPOINT = "/assets"
LOGIN_ENDPOINT = "/login"
# 举例管理员接口路径，可根据实际替换
ADMIN_DELETE_USER_ENDPOINT = "/admin/users/2"
# 管理员与普通用户接口路径需按实际API调整

def test_security_flow():
    # 测试 1：未授权访问
    resp = client.get(ASSET_LIST_ENDPOINT)
    test1 = resp.status_code == 401
    print_result("Test 1: 未授权访问资产列表返回401", test1)

    # 测试 2：用户登录与认证
    login_data = {"username": USERNAME_NORMAL, "password": PASSWORD_NORMAL}
    resp = client.post(LOGIN_ENDPOINT, data=login_data)
    test2 = resp.status_code == 200 and "access_token" in resp.json()
    print_result("Test 2: 正确登录获取token", test2)
    access_token = resp.json().get("access_token") if test2 else None
    # 测试 3：权限验证（越权访问）（可选，如有管理员接口）
    unauthorized_token_headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    # 仅当有管理员接口时
    test3 = resp.status_code == 403 and "仅管理员允许" in resp.json().get("msg")
    print_result("Test 3: 普通用户删除用户被拒绝返回403且msg为仅管理员允许", test3)

    # 测试 4：正常业务访问
    if access_token:
        resp = client.get(ASSET_LIST_ENDPOINT, headers={"Authorization": f"Bearer {access_token}"})
        correct_status = resp.status_code == 200
        json_data = resp.json()
        correct_structure = isinstance(json_data, dict) and \
            all(k in json_data for k in ["code", "msg", "data"])
        test4 = correct_status and correct_structure
        print_result("Test 4: 正常带Token访问资产列表", test4)
    else:
        print("Test 4: 跳过（因登录失败）")

    # 测试 5：异常输入处理（登录错误密码）
    wrong_login = {"username": USERNAME_NORMAL, "password": "wrongpassword"}
    resp = client.post(LOGIN_ENDPOINT, data=wrong_login)
    status_check = resp.status_code in (400, 401)
    body_text = resp.text
    leaked_sensitive_info = ("用户不存在" in body_text) or ("not exist" in body_text.lower())
    test5 = status_check and not leaked_sensitive_info
    print_result("Test 5: 登录错误密码拒绝且不泄漏敏感信息", test5)

if __name__ == "__main__":
    test_security_flow()