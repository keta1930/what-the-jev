const dollars = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumSignificantDigits: 15,
});

export const formatCost = (cost) => dollars.format(cost);
