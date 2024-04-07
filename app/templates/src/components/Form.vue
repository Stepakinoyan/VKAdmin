
<template>
    <div class="flex items-center justify-center h-screen">
    <form class="space-y-0.5">
      <InputGroup>
          <InputGroupAddon>
              <i class="pi pi-user"></i>
          </InputGroupAddon>
          <InputText placeholder="ФИО"/>
      </InputGroup>
      <InputGroup>
          <InputGroupAddon>
              <i class="pi pi-phone"></i>
          </InputGroupAddon>
          <InputMask mask="+7 (999) 999-99-99"/>
      </InputGroup>
      <InputGroup>
          <InputGroupAddon>
              <i class="pi pi-at"></i>
          </InputGroupAddon>
          <InputText placeholder="email@gmail.com" />
      </InputGroup>
      <InputGroup class="mt-1 flex justify-center ">
        <Button label="Войти"/>
      </InputGroup>
    </form>
    </div>


</template>
