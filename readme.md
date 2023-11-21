# AWS
> 해당 프로젝트에서는 AWS 에서 사용한 lambda function 을 기술

## ECS
> Stage Cluster 의 경우 주말동안 사용하지 않도록 python boto3 를 이용하여 작성 후 Eventbridge 를 통해 스케쥴링
>> - [ecs/stage-ecs-on.py](ecs/stage-ecs-on.py)
>> - [ecs/stage-ecs-off.py](ecs/stage-ecs-off.py)

## WAFv2
> 이벤트 랜딩 페이지의 구글 광고 검수를 위해 waf 장비에 명시적 구글봇을 자동으로 추가하도록 구성
>> - [waf/waf-googlebot-ipset.py](waf/waf-googlebot-ipset.py)
