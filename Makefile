.PHONY: build
app=rongliang_algorithm_serving_applet_cloud
legacy_image=$(shell docker images --filter=reference="*rongliang_algorithm_serving_applet_cloud*" -q)
version=$(shell date '+%Y%m%d%H%M')
build:
ifeq ($(strip $(legacy_image)),)
	@echo "nope"
else
	docker rmi -f ${legacy_image}
endif
	docker buildx build --platform linux/amd64 -t ${app} .
# 	docker login --username=trsopenapi@1219654161317312 registry.cn-beijing.aliyuncs.com/saasalpha/tmaster --password=AlipaySaas22
# 	docker tag ${app} registry.cn-beijing.aliyuncs.com/saasalpha/tmaster:ats_${app}_$(version)
# 	docker push registry.cn-beijing.aliyuncs.com/saasalpha/tmaster:ats_${app}_$(version)