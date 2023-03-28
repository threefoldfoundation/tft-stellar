<script lang="ts">
  import Input from '../ui/Input.svelte';
  import Alert from '../ui/Alert.svelte';
  import { validatePrivateKey } from '../../utils/validations';
  import { activatePKStore, alertStore } from '../../utils/stores';

  let privateKeyValue: string;
  let isLoading: boolean;
  let isSigned: boolean;

  const onKeypress = (e) => {
    if (e.keyCode === 13) {
      if (validatePrivateKey(privateKeyValue).isValid) {
        isLoading = true;
        isSigned = true;
      }
    }
    console.log(e);
  };

  $: privateKeyValue, (isSigned = false);
</script>

<div class="container">
  <div class="lock">
    <div class="alert w-100 mb-4 text-start">
      <h4>
        Second Screen | <span class="text-primary">Validate Private Key</span>
      </h4>
      Selected address :
      <span class="text-primary">
        {$activatePKStore.address}
      </span>
    </div>
    <div class="row w-100">
      <div class="col-8">
        <Input
          bind:value={privateKeyValue}
          label="Wallet Private Key"
          validation={validatePrivateKey}
          className={'pk-input'}
          bind:isLoading
          onKeyPress={(e) => onKeypress(e)}
        />
        {#if $alertStore.isOpen}
          <Alert
            message={$alertStore.message}
            isOpen={$alertStore.isOpen}
            className={$alertStore.className}
          />
        {/if}
      </div>
      <div class="col-4">
        {#if isSigned}
          <i class="fa-solid fa-lock-open unlocked" />
        {:else}
          <i class="fa-solid fa-lock locked" />
        {/if}
      </div>
    </div>
  </div>
</div>
