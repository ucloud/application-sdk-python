## API参考文档

主要的API参考文档如下：

#### from iotedgeapplicationlinksdk
* **[getLogger()](#getLogger)**

---

#### from iotedgeapplicationlinksdk.client
* **[get_application_config()](#get_application_config)**
* **[get_application_name()](#get_application_name)**
* **[get_gateway_product_sn()](#get_gateway_product_sn)**
* **[get_gateway_device_sn()](#get_gateway_device_sn)**
* **[publish()](#publish)**
* **[register_callback()](#register_callback)**


---
<a name="getLogger"></a>
### getLogger()
返回应用内置logger。

---
<a name="get_application_config"></a>
### get_application_config()
返回应用配置。

---
<a name="get_application_name"></a>
### get_application_name()
返回应用名称。

---
<a name="get_gateway_product_sn"></a>
### get_gateway_product_sn()
返回应用网关ProductSN。

---
<a name="get_gateway_device_sn"></a>
### get_gateway_device_sn()
返回应用网关DeviceSN。

---
<a name="publish"></a>
### publish()
上报消息到Link IoT Edge。参数(topic: str, payload: bytes)

* topic`str`: 上报消息到Link IoT Edge的mqtt topic。
* payload`bytes`: 上报消息到Link IoT Edge的消息内容

---
<a name="register_callback"></a>
### register_callback
设置应用接收消息的回调函数，参数(cb, rrpc_cb)

* cb`func`: 应用消息回调，例如：` def callback(topic:str, msg:bytes): print(str(msg,'utf-8')`
* rrpc_cb`func`: 应用RRPC消息回调，例如：` def callback(topic:str, msg:bytes): print(str(msg,'utf-8')`
