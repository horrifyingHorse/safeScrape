interface CliState {
  status: boolean,
}

export const scrapeState: CliState = $state({
  status: false
});
