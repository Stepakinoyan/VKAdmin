<template>
    <Card class="border border-gosuslugi-border">
        <template #title>После изменений данных паспорта в личном кабинете они должны пройти проверку в МВД</template>
        <template #content>
            <div class="space-y-8">
                        <div>
                            <ol class="space-y-2 list-decimal list-inside blue-digital-marker">
                                <h3 class="text-xl font-bold">Как изменить данные паспорта</h3>
                                <li class="text-lg"><a href="#" class="text-blue-700 hover:text-blue-600">Войдите на Госуслуги</a></li>
                                <li class="text-lg">Перейдите в личный кабинет → <a href="#" class="text-blue-600">Личные документы</a></li>
                                <li class="text-lg">Откройте карточку «Паспорт РФ» → нажмите «Редактировать»</li>
                                <li class="text-lg">Внесите изменения и нажмите «Сохранить»</li>
                            </ol>    
                        </div>
                        <h3 class="text-xl font-bold">Сколько длится проверка паспорта</h3>
                        <div class="space-y-3">
                            <p class="text-lg">Если добавили или изменили данные паспорта, проверка может занять до 5 календарных дней. Если она длится дольше, <a href="#" class="text-blue-600">обратитесь в службу поддержки Госуслуг</a> . К обращению прикрепите скриншот проблемы</p>
                            <ul>
                                <li><a href="#" class="text-lg text-blue-700 hover:text-blue-600">Изменить паспортные данные</a></li>
                                <li><a href="#" class="text-lg text-blue-700 hover:text-blue-600">Найти МВД</a></li>
                                <li><a href="#" class="text-lg text-blue-700 hover:text-blue-600">Что такое паспорт</a></li>
                            </ul>
                        </div>
                    </div>
        </template>
    </Card>
</template>

<style>
.blue-digital-marker li::marker {
    color: #0d4cd3;
    font-weight: 700;
}
</style>