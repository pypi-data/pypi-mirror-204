### ABAC Engine
Thư viện xử lý kiểm tra quyền theo logic ABAC (Attribute-based access control).


### Cài đặt:
```bash
 $ pip3 install m-abac
 ```

### Sử dụng:

##### Kiểm tra user có quyền thao tác hay không:
   ```python
    from m_abac import PolicyDecisionPoint
    merchant_id = "1b99bdcf-d582-4f49-9715-1b61dfff3924"
    resource = "deal"
    # action = "UpdateFromSale"
    action = "ListFromSale"
    account_id = "704eac91-7416-497f-a17d-d81cfa2d3211"
    # thông tin user ko có thì để None 
    user_info = {
        "block": "KHDN",
        "scope_code": "MB##HN"
    }
    request_access = {
        "deal": {
            # "block": "KHCN",
            # "scope_code": "MB##HN##CAU_GIAY"
        }
    }

    pdb = PolicyDecisionPoint(merchant_id=merchant_id, resource=resource, action=action, account_id=account_id,
                              user_info=user_info, request_access=request_access)
    result = pdb.is_allowed()
    if not result.get_allow_access():
        # trả về lỗi không có quyền truy cập 
   ```
#### Log - 1.0.0
    - release sdk
    