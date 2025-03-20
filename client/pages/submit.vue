<template>
    <section class="get-in-touch">
      <h1 class="title">
        ВИС-2
      </h1>
      <form
        class="contact-form row"
        @submit.prevent="handleSubmit"
      >
        <div class="form-field col-lg-6">
          <input
            id="firstName"
            v-model="form.firstName"
            :class="{ 'not-empty': form.firstName.length > 0 }"
            class="input-text js-input"
            type="text"
            required
          >
          <label
            class="label"
            for="firstName"
          >Собствено име</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="lastName"
            v-model="form.lastName"
            :class="{ 'not-empty': form.lastName.length > 0 }"
            class="input-text js-input"
            type="text"
            required
          >
          <label
            class="label"
            for="lastName"
          >Фамилно име</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="phone"
            v-model="form.phone"
            class="input-text js-input"
            :class="{ 'not-empty': form.phone.length > 0 }"
            type="text"
            required
          >
          <label
            class="label"
            for="phone"
          >Телефонен номер</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="amount"
            v-model="form.amount"
            class="input-text js-input"
            :class="{ 'not-empty': form.amount.length > 0 }"
            type="text"
            required
          >
          <label
            class="label"
            for="amount"
          >Дължима сума</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="familyStatus"
            v-model="form.familyStatus"
            class="input-text js-input"
            :class="{ 'not-empty': form.familyStatus.length > 0 }"
            type="text"
            required
          >
          <label
            class="label"
            for="familyStatus"
          >Семейно положение</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="income"
            v-model="form.income"
            :class="{ 'not-empty': form.income.length > 0 }"
            class="input-text js-input"
            type="text"
            required
          >
          <label
            class="label"
            for="income"
          >Доход</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="egn"
            v-model="form.egn"
            :class="{ 'not-empty': form.egn.length > 0 }"
            class="input-text js-input"
            type="text"
            required
          >
          <label
            class="label"
            for="egn"
          >ЕГН</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="creditExpiry"
            v-model="form.creditExpiry"
            class="input-text js-input"
            :class="{ 'not-empty': form.creditExpiry.length > 0 }"
            type="text"
            required
          >
          <label
            class="label"
            for="creditExpiry"
          >Дата на изтичане на кредита</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="address"
            v-model="form.address"
            class="input-text js-input"
            :class="{ 'not-empty': form.address.length > 0 }"
            type="text"
            required
          >
          <label
            class="label"
            for="address"
          >Адрес</label>
        </div>
        <div class="form-field col-lg-6">
          <input
            id="age"
            v-model="form.age"
            class="input-text js-input"
            :class="{ 'not-empty': form.age.length > 0 }"
            type="text"
            required
          >
          <label
            class="label"
            for="age"
          >Възраст</label>
        </div>
        <div class="form-field col-lg-12">
          <textarea
            id="job"
            v-model="form.job"
            :class="{ 'not-empty': form.job.length > 0 }"
            class="input-text js-input"
            type="text"
            required
          />
          <label
            class="label"
            for="job"
          >Работа</label>
        </div>
        <div class="form-field col-lg-12">
          <input
            class="submit-btn"
            type="submit"
            value="Изпрати"
          >
        </div>
      </form>
      <p v-if="responseMessage" class="response-paragraph">{{ responseMessage }}</p>
    </section>
  </template>

  <script setup>
  const form = ref({
    firstName: '',
    lastName: '',
    phone: '',
    amount: '',
    familyStatus: '',
    income: '',
    egn: '',
    creditExpiry: '',
    address: '',
    age: '',
    job: '',
  })

  const responseMessage = ref('')

  async function handleSubmit() {
    try {
      const res = await $fetch('http://localhost:3000/api/submit', {
        method: 'POST',
        body: form.value,
      })
      console.log('Form submitted successfully:', res)

      responseMessage.value = 'Формата беше изпратена успешно!'

      form.value = {
        firstName: '',
        lastName: '',
        phone: '',
        amount: '',
        familyStatus: '',
        income: '',
        egn: '',
        creditExpiry: '',
        address: '',
        age: '',
        job: '',
      }
    }
    catch (error) {
      console.error('Error submitting form:', error)
      responseMessage.value = 'Възникна грешка при изпращането на формата.'
    }
  }
  </script>

  <style scoped>
  .get-in-touch {
    max-width: 800px;
    margin: 50px auto;
    position: relative;
  }

  .get-in-touch .title {
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 3.2em;
    line-height: 48px;
    padding-bottom: 48px;
    color: #be1515;
    background: #be1515;
    background: -moz-linear-gradient(left, #4e3c3c 0%, #be1515 100%) !important;
    background: -webkit-linear-gradient(left, #4e3c3c 0%, #be1515 100%) !important;
    background: linear-gradient(to right, #4e3c3c 0%, #be1515 100%) !important;
    background-clip: text !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
  }

  .response-paragraph {
    text-align: center;
    font-size: 1.5em;
    color: #be1515;
    background: -moz-linear-gradient(left, #4e3c3c 0%, #be1515 100%);
    background: -webkit-linear-gradient(left, #4e3c3c 0%, #be1515 100%);
    background: linear-gradient(to right, #4e3c3c 0%, #be1515 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 20px;
  }

  .contact-form .form-field {
    position: relative;
    margin: 32px 0;
  }
  .contact-form .input-text {
    display: block;
    width: 100%;
    height: 36px;
    border-width: 0 0 2px 0;
    border-color: #b82c06;
    font-size: 18px;
    line-height: 26px;
    font-weight: 400;
    resize: none;
  }
  .contact-form .input-text:focus {
    outline: none;
  }
  .contact-form .input-text:focus + .label,
  .contact-form .input-text.not-empty + .label {
    -webkit-transform: translateY(-24px);
            transform: translateY(-24px);
  }
  .contact-form .label {
    position: absolute;
    left: 20px;
    bottom: 11px;
    font-size: 18px;
    line-height: 26px;
    font-weight: 400;
    color: #391107;
    cursor: text;
    transition: -webkit-transform .2s ease-in-out;
    transition: transform .2s ease-in-out;
    transition: transform .2s ease-in-out,
    -webkit-transform .2s ease-in-out;
  }
  .contact-form .submit-btn {
    display: inline-block;
    background-color: #000;
     background-image: linear-gradient(125deg,#be1515,#4e3c3c);
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 16px;
    padding: 8px 16px;
    border: none;
    width:200px;
    cursor: pointer;
  }

  .form-field.col-lg-12 {
    text-align: center;
  }

  .contact-form .submit-btn {
    display: inline-block;
    background-color: #000;
    background-image: linear-gradient(125deg, #be1515, #4e3c3c);
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 16px;
    padding: 8px 16px;
    border: none;
    width: 200px;
    cursor: pointer;
  }
  </style>
