<script lang="ts">
  import { activatePKStore } from '../../utils/stores';
  import Navbar from '../ui/Navbar.svelte';
  import ValidateAddress from './ValidateAddress.svelte';
  import ValidatePrivateKey from './ValidatePrivateKey.svelte';
</script>

<Navbar />
{#if !$activatePKStore.isSelected}
  <ValidateAddress />
{:else}
  <ValidatePrivateKey />
{/if}
