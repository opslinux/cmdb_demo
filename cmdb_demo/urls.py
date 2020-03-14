"""cmdb_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.conf.urls import url
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]
from django.urls import path, include
from app_demo.views import UUIDDetail, ServerDetail, SecurityDeviceDetail, NetworkDeviceDetail, ManufactoryDetail, \
    EventLogDetail, AssetDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uuid/', UUIDDetail),
    # path('v1/cmdb/', include('app_demo.urls')),
    path('v1/cmdb/server/', ServerDetail),
    path('v1/cmdb/security/device/', SecurityDeviceDetail),
    path('v1/cmdb/network/device/', NetworkDeviceDetail),
    path('v1/cmdb/manufactory/', ManufactoryDetail),
    path('v1/cmdb/event/log/', EventLogDetail),
    path('v1/cmdb/asset/', AssetDetail)
]

