<script setup>
import Menu from '../components/Menu.vue'
import Instruction from '../components/Instruction.vue'
import Article from '../components/Article.vue'
</script>

<template>
    <div>
        <header>
            <Menu/>
        </header>
        <main class="flex flex-col lg:flex-row lg:container mx-3 lg:mx-auto mt-5 lg:space-x-5 space-y-6">
            <section class="w-full lg:w-8/12 space-y-10">
                <div>
                    <h2 class="text-[32px] mb-4 leading-10">
                        Как изменить данные паспорта в личном кабинете
                    </h2>
                    <Instruction/>
                </div>
                <div >
                    <h2 class="text-[32px] leading-10">Другие статьи категории 
                        <a href="#" class="text-blue-700 hover:text-blue-600">Личные документы</a>
                    </h2>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full lg:w-11/12 xl:w-10/12 mt-6 lg:mt-10">
                        <Article title="Получение загранпаспорта" :items="['Зачем нужен загранпаспорт', 'Как заказать загранпаспорт на Госуслугах', 'На кого можно оформить загранпаспорт']" class="pb-14"/>
                        <Article title="Постоянная регистрация" :items="['Зачем нужна прописка', 'Как оформить прописку', 'Что нужно для оформления прописки на Госуслугах']" class="pb-14"/>
                        <Article title="Временная регистрация" :items="['Зачем нужна временная регистрация', 'Как оформить временную регистрацию', 'Временная регистрация в МВД и МФЦ']" class="pb-14"/>
                        <Article title="Получение СНИЛС" :items="['Что такое СНИЛС и зачем он нужен', 'Как оформить СНИЛС', 'Как получить СНИЛС ребёнка']" class="pb-14"/>
                        <Article title="Получение ИНН" :items="['Как оформить ИНН ребёнку', 'Если ИНН не найден', 'Как восстановить свидетельство ИНН онлайн']" class="pb-14"/>
                        <Article title="Перемена имени" :items="['Как сменить ФИО', 'Сколько длится регистрация перемены имени', 'Согласие органов опеки на смену имени ребёнка']" class="pb-14"/>
                    </div>
                </div>
            </section>
            <section class="w-full lg:w-1/4">
                <Card class="sticky lg:fixed bg-gosuslugi border-0 shadow-none max-w-full lg:w-[20rem] mr-5" style="overflow: hidden;">
                    <template #title class="text-[18px] leading-6">Другие вопросы по теме<br>Получение паспорта РФ</template>
                    <template #content>
                        <ul class="space-y-4">
                            <li><a href="#" class="text-blue-700 hover:text-blue-600">Что такое паспорт</a></li>
                            <li><a href="#" class="text-blue-700 hover:text-blue-600">Что указывают в паспорте</a></li>
                            <li><a href="#" class="text-blue-700 hover:text-blue-600">Размер госпошлины при получении паспорта</a></li>
                            <li><a href="#" class="text-blue-700 hover:text-blue-600">Штрафы за паспорт</a></li>
                            <li><a href="#" class="text-blue-700 hover:text-blue-600">Когда нужно получать и менять паспорт</a></li>
                        </ul>
                    </template>
                </Card>
            </section>
        </main>
        <footer class="flex justify-start lg:justify-center w-full bg-soft-blue mt-10">
            <div class="flex flex-col lg:flex-row justify-around w-full lg:w-1/2 py-12 space-y-8 lg:space-y-0 mx-8">
                <ul class="space-y-3 text-grey-blue">
                    <li class="text-xl"><a href="#" class="hover:text-black">Личный кабинет</a></li>
                    <li class="text-xl"><a href="#" class="hover:text-black">Регистрация</a></li>
                    <li class="text-xl"><a href="#" class="hover:text-black">Контакты</a></li>
                </ul>
                <ul class="space-y-3 text-grey-blue">
                    <li class="text-xl"><a href="#" class="hover:text-black">Как найти услугу</a></li>
                    <li class="text-xl"><a href="#" class="hover:text-black">Помощь</a></li>
                    <li class="text-xl"><a href="#" class="hover:text-black">Карта центров обслуживания</a></li>
                </ul>
                <ul class="space-y-3 text-grey-blue">
                    <li class="text-xl"><a href="#" class="hover:text-black">Партнёрам</a></li>
                    <li class="text-xl"><a href="#" class="hover:text-black">Для иностранцев</a></li>
                    <li>
                        <a href="#" class="flex flex-row text-xl space-x-3 hover:text-black">
                            <i class="pi pi-send pt-[5px] lg:text-lg"></i>
                            <span>г Благовещенск</span>                            
                        </a>
                    </li>
                </ul>
            </div>
        </footer>

    </div>
</template>


