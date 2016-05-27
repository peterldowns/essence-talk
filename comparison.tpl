<!doctype HTML>
<html>

<head>
  <title> Results Comparison </title>
  <style>
    body {
      font-size: 16px;
      font-family: 'Times New Roman';
    }
    table {
      width: 100%;
      box-sizing: border-box;
      text-align: left;
    }
    td {
      padding: 10px;
    }
    .weight {
      font-weight: bold;
      font-size: 14px;
    }
    
  </style>
</head>

<body>
  <center><h1>Bookshrink</h1></center>
  <table>
    <tr>
      <th> Relative </th>
      <th> Sentence </th>
    </tr>
    {{#bs}}
      <tr>
        <td class="weight"> {{relative}} </td>
        <td> {{sentence}} </td>
      </tr>
    {{/bs}}
  </table>
  <center><h1>Singular Value Decomposition</h1></center>
  <table>
    <tr>
      <th> Relative </th>
      <th> Sentence </th>
    </tr>
    {{#svd}}
      <tr>
        <td class="weight"> {{relative}} </td>
        <td> {{sentence}} </td>
      </tr>
    {{/svd}}
  </table>
</body>

</html>
