function deletePurchase(purchaseId) {
  fetch("/delete-purchase", {
    method: "POST",
    body: JSON.stringify({ purchaseId : purchaseId }),
  }).then((_res) => {
    window.location.href = "http://192.168.178.241:5000/purchase";
  });
}
