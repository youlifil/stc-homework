# Тестовое для СТЦ
Пока реализован сам расчёт и запуск из командной строки. Решалка берёт входные параметры заданий из конфигурационного файла в формате json.

*Полную версию с FastAPI сервером и веб-интерфейсом дам после выходных. В рабочие дни на неделе было ужасно мало времени.*

## Установка
```bash
python -m venv .venv
pip install -r requirements.txt
. .venv/bin/activate
```
## Входные данные
`data/STARLINK.txt` - TLE-файл с данными спутников

`data/situation-A.txt` - конфигурация для заданий 1 и 2

`data/situation-B.txt` - конфигурация для задания 3
## Запуск
### Задания 1 и 2
`python main.py --satellites=data/STARLINK.txt --config=data/situation-A.json`

### Задание 3
`python main.py --satellites=data/STARLINK.txt --config=data/situation-B.json`

## Результаты
### Задания 1 и 2
Используется шаг времени 1 сек. За 1 сек угловое смещение спутника ~1-2 градуса, так что при угле обзора 70° такой шаг вполне приемлем, чтобы ничего не потерять. На моём компе считает это задание меньше чем за 2 сек.
```
             name  norad_id
0   STARLINK-1741     46567
1   STARLINK-2464     48123
2   STARLINK-2139     48554
3   STARLINK-2667     48663
4   STARLINK-3113     49735
5   STARLINK-4006     52676
6   STARLINK-3962     52708
7   STARLINK-4533     53406
8   STARLINK-6345     56790
9  STARLINK-31437     60057
Найдено видимых спутников: 10
Ближайший видимый спутник:
NORAD ID: 60057, NAME: STARLINK-31437
Когда был виден: 2025-05-18 16:20:20+03:00
Расстояние: 558.29 км
Угол места (altitude): 58.26°
Азимут: 293.72°
```
### Задание 3
В конфиге для этого задания задан шаг времени 2 сек. Так считает долговато (в районе 20 сек), но зато находит все спутники. При б**о**льших значениях шага будет считать быстрее, но число найденных спутников будет меньше, т.к. поле зрения в этом задании очень маленькое.
```
                    name  norad_id
0          STARLINK-1279     45360
1          STARLINK-1301     45361
2          STARLINK-1267     45384
3          STARLINK-1297     45395
4          STARLINK-1307     45397
5          STARLINK-1259     45403
6          STARLINK-1298     45413
7          STARLINK-1309     45414
8          STARLINK-1517     45787
9          STARLINK-1523     46028
10         STARLINK-1526     46029
11         STARLINK-1730     46563
12         STARLINK-2116     47724
13         STARLINK-2418     48097
14         STARLINK-2443     48107
15         STARLINK-2459     48119
16         STARLINK-2473     48131
17         STARLINK-2700     48431
18         STARLINK-2680     48432
19         STARLINK-2699     48433
20         STARLINK-2139     48554
21         STARLINK-2145     48555
22         STARLINK-2151     48556
23         STARLINK-2214     48566
24         STARLINK-2241     48586
25         STARLINK-2245     48589
26         STARLINK-2250     48593
27         STARLINK-2757     48604
28         STARLINK-2732     48646
29         STARLINK-3233     49746
30         STARLINK-3229     49751
31         STARLINK-3349     50813
32         STARLINK-3952     52534
33         STARLINK-3958     52535
34         STARLINK-3964     52536
35         STARLINK-3845     52541
36         STARLINK-3858     52553
37         STARLINK-3836     52577
38         STARLINK-3893     52579
39         STARLINK-3919     52580
40         STARLINK-4084     52657
41         STARLINK-4064     52665
42         STARLINK-4076     52667
43         STARLINK-4067     52668
44         STARLINK-4073     52672
45         STARLINK-3934     52675
46         STARLINK-4005     52686
47         STARLINK-3993     52692
48         STARLINK-3946     52693
49         STARLINK-4018     52697
50         STARLINK-4033     52702
51         STARLINK-4007     52707
52         STARLINK-3683     53167
53         STARLINK-4300     53173
54         STARLINK-4258     53180
55         STARLINK-4534     53395
56         STARLINK-4515     53397
57         STARLINK-4528     53399
58         STARLINK-5092     55408
59        STARLINK-30549     58030
60        STARLINK-31529     59000
61        STARLINK-31990     60024
62        STARLINK-32005     60034
63        STARLINK-31775     60052
64        STARLINK-31735     60054
65        STARLINK-31825     60056
66        STARLINK-32175     60339
67        STARLINK-32176     60340
68        STARLINK-32428     61666
69        STARLINK-32417     61673
70        STARLINK-32326     61674
71  STARLINK-11336 [DTC]     61698
72  STARLINK-11296 [DTC]     61699
73        STARLINK-32404     61710
74        STARLINK-32467     61713
75        STARLINK-32465     61716
76        STARLINK-32322     61720
77        STARLINK-32438     61722
78  STARLINK-11402 [DTC]     61874
Найдено видимых спутников: 79
```
