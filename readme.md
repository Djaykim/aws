# AWS
> 해당 프로젝트에서는 AWS 에서 사용한 기술들을 요약

## ECS
> Stage Cluster 의 경우 주말동안 사용하지 않도록 python boto3 를 이용하여 작성 후 Eventbridge 를 통해 스케쥴링
>> - [ecs/stage-ecs-on.py](ecs/stage-ecs-on.py)
>> - [ecs/stage-ecs-off.py](ecs/stage-ecs-off.py)

## WAFv2
> 이벤트 랜딩 페이지의 구글 광고 검수를 위해 waf 장비에 명시적 구글봇을 자동으로 추가하도록 구성
>> - [waf/waf-googlebot-ipset.py](waf/waf-googlebot-ipset.py)

## DynamoDB
> - SOAP Req/Res 통신 전문 그대로를 저장하고 백오피스에서 필요시 조회하고자 함. 
> - 설정 참고 URL : https://techblog.woowahan.com/2633/
> - 온디맨드 용량 : 워크로드의 읽기/쓰기, 트래픽의 예측이 불가능 할 경우
> - 프로비저닝 용량 : 트래픽이 일관되어 예측이 가능할 경우
>> 온디맨드 용량을 설정하여 구성 후 부하테스트 등을 통해 프로비저닝 + Auto Scaling