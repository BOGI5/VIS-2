<template>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>EGN</th>
            <th>Amount</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data" :key="index">
            <td>{{ item.firstName }}</td>
            <td>{{ item.lastName }}</td>
            <td>{{ item.egn }}</td>
            <td>{{ item.amount }}</td>
            <td>{{ item.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script setup>
  import { ref } from 'vue';

  const data = ref([
    {
      firstName: 'sss',
      lastName: 'sss',
      egn: '12345',
      amount: '10',
      date: '10.19.1919',
    },
    {
      firstName: 'sss',
      lastName: 'sss',
      egn: '12345',
      amount: '10',
      date: '10.19.1919',
    },
    {
      firstName: 'sss',
      lastName: 'sss',
      egn: '12345',
      amount: '10',
      date: '10.19.1919',
    },
  ]);
  </script>

  <style scoped>
  .table-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: white;
  }

  table {
    border-collapse: collapse;
    width: 80%;
    text-align: center;
    border: 5px solid;
    border-image-source: linear-gradient(to right, red, black);
    border-image-slice: 1;
  }

  th,
  td {
    border: 2px solid black; /* Ensures uniform thickness inside */
    padding: 10px;
    background-color: white;
  }

  th {
    background-color: #f4f4f4;
    font-weight: bold;
  }
  </style>
