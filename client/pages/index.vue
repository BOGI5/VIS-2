<template>
  <div class="container">
    <h1 class="text-primary">Home</h1>
    <button class="btn btn-success mb-3">Button</button>

    <form class="mb-4" @submit.prevent="handleFormSubmit">
      <div class="mb-3">
        <label for="firstName" class="form-label">Собствено име</label>
        <input
          id="firstName"
          v-model="formData.firstName"
          type="text"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="lastName" class="form-label">Фамилно име</label>
        <input
          id="lastName"
          v-model="formData.lastName"
          type="text"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="phoneNumber" class="form-label">Телефонен номер</label>
        <input
          id="phoneNumber"
          v-model="formData.phoneNumber"
          type="tel"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="dueDate" class="form-label">Дата на погасяване</label>
        <input
          id="dueDate"
          v-model="formData.dueDate"
          type="date"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="amount" class="form-label">Сума</label>
        <input
          id="amount"
          v-model="formData.amount"
          type="number"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Изпрати</button>
    </form>

    <table class="table table-striped table-bordered">
      <thead class="table-primary">
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Phone Number</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(person, index) in people" :key="index">
          <td>{{ person.firstName }}</td>
          <td>{{ person.lastName }}</td>
          <td>{{ person.phoneNumber }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const people = ref([
  { firstName: 'John', lastName: 'Doe', phoneNumber: '123-456-7890' },
  { firstName: 'Jane', lastName: 'Smith', phoneNumber: '987-654-3210' },
  { firstName: 'Alice', lastName: 'Johnson', phoneNumber: '555-123-4567' },
])

const formData = ref({
  firstName: '',
  lastName: '',
  phoneNumber: '',
  dueDate: '',
  amount: '',
})

async function handleFormSubmit() {
  try {
    const res = await $fetch('http://localhost:3000/api/submit', {
      method: 'POST',
      body: formData.value,
    })
    console.log('Form submitted successfully:', res)

    formData.value = {
      firstName: '',
      lastName: '',
      phoneNumber: '',
      dueDate: '',
      amount: '',
    }
  } catch (error) {
    console.error('Error submitting form:', error)
  }
}
</script>
