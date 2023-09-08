$(document).ready(function () {
  const username = document.getElementById("top-username").textContent
  const url_ = 'https://www.dulgan.tech/api/v1/' + username + '/contracts'
  $(function () {
    $.ajax({
      type: 'GET',
      url: url_,
      contentType: 'application/json',
      dataType: 'json',
      success: function (contract) {
	const contractAsB = contracts['Contracts_buyer'];
	const contractAsS = contracts['Contracts_seller'];
	for (const i in contractAsS) {
          $("tbody#seller").html(`<tr>
                    <td>${contractAsS[i]['id']}</td>
                    <td>
                    <a href="https://dulgan.tech/contracts/${contractAsS[i]['id']}">
                    ${contractAsS[i]['name']}
                    </a>
                    </td>
                    <td>${contractAsS[i]['description']}</td>
                    <td>${contractAsS[i]['amount']}</td>
                    <td>${contractAsS[i]['user_as_b']}</td>
                    <td>${contractAsS[i]['user_as_s']}</td>
                    <td>${contractAsS[i]['created_at']}</td>                                                <td>${contractAsS[i]['status']}<td>
                  </tr>`);
	}
        for (const i in contractAsB) {
          $("tbody#buyer").html(`<tr>
                    <td>${contractAsB[i]['id']}</td>
                    <td>
		    <a href="https://dulgan.tech/contracts/${contractAsB[i]['id']}">
		    ${contractAsB[i]['name']}
		    </a>
		    </td>
                    <td>${contractAsB[i]['description']}</td>
		    <td>${contractAsB[i]['amount']}</td>
                    <td>${contractAsB[i]['user_as_b']}</td>
                    <td>${contractAsB[i]['user_as_s']}</td>
		    <td>${contractAsB[i]['created_at']}</td>
		    <td>${contractAsB[i]['status']}<td>
		  </tr>`);
	}
      }
    });
  });
})
