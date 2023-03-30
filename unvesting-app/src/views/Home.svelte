<script lang="ts">
  import AddressScreen from '../components/home/AddressScreen.svelte';
  import SecretScreen from '../components/home/SecretScreen.svelte';
  import { activatePKStore } from '../utils/stores';
</script>

{#if !$activatePKStore.isSelected}
  <AddressScreen />
{:else}
  <SecretScreen />
{/if}

<svelte:head>
  <title>Unvest TFT</title>
</svelte:head>
