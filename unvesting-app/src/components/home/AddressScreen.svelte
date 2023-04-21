<script lang="ts">
  import Navbar from './Navbar.svelte';
  import Input from '../ui/Input.svelte';
  import { validateAddress } from '../../utils/validations';
  import http from '../../utils/axios';
  import type { OnResponseVestingAccounts } from '../../utils/types';
  import { activatePKStore, alertStore } from '../../utils/stores';
  import Alert from '../ui/Alert.svelte';

  let addressValue: string;
  let isLoading: boolean;
  let vestingAccounts: OnResponseVestingAccounts;

  const onKeypress = async (e: { keyCode: number }) => {
    if (e.keyCode === 13) {
      // Enter pressed.
      if (validateAddress(addressValue).isValid) {
        isLoading = disabled = true;
        // disabled = true;
        await http
          .post('vesting_accounts', { owner_address: addressValue })
          .then((res) => {
            if (res) {
              vestingAccounts = res.data;
              if (vestingAccounts && !vestingAccounts.vesting_accounts.length) {
                alertStore.set({
                  message: 'No vested TFT found for this address',
                  isOpen: true,
                  className: 'info',
                });
              } else if (vestingAccounts.Error) {
                alertStore.set({
                  message: vestingAccounts.Error,
                  isOpen: true,
                  className: 'danger',
                });
              } else {
                $alertStore.isOpen = false;
              }
            }
          });
        isLoading = disabled = false;
      }
    }
  };

  const activatePrivateKey = () => {
    activatePKStore.set({
      selectedAddress: vestingAccounts.vesting_accounts[0].address,
      ownerAddress: vestingAccounts.owner_adress,
      isSelected: true,
    });
  };

  $: disabled = !validateAddress(addressValue).isValid;
</script>

<Navbar />
<div class="container height-100">
  <div class="d-flex justify-content-center align-items-center home-card">
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title d-flex justify-content-center">
          <span class="screen-view-dot">1</span>
          Check for vested TFT
        </h5>
        <hr />
        <div class="row">
          <div class="col-12 padding-left-none padding-right-none">
            <Input
              bind:value={addressValue}
              label="Wallet Address"
              validation={validateAddress}
              className={'address-input'}
              bind:isLoading
              onKeyPress={(e) => onKeypress(e)}
              placeholder={''}
            />
          </div>
        </div>
        {#if $alertStore.isOpen}
          <Alert
            message={$alertStore.message}
            isOpen={$alertStore.isOpen}
            className={$alertStore.className}
          />
        {/if}
        <div class="btns d-flex justify-content-end">
          <button
            {disabled}
            on:click={() => {
              onKeypress({ keyCode: 13 });
            }}
            class="btn btn-success ml-btn-action"
          >
            Search
            <i class="fas fa-search" />
          </button>
        </div>
        {#if vestingAccounts && !vestingAccounts.Error}
          {#if vestingAccounts.vesting_accounts.length}
            {#each vestingAccounts.vesting_accounts as account}
              <div class="card mt-4 mb-5">
                <div class="card-body">
                  <div class="row">
                    <div class="col-12">
                      <strong>
                        {Math.round((+account.TFT + Number.EPSILON) * 100) /
                          100} vested TFT
                      </strong>
                    </div>
                    <div class="col-12 mb-4">
                      <p class="mb-0">
                        on escrow account {account.address}
                      </p>
                    </div>
                  </div>
                  <button
                    class="btn use-btn w-100 btn-use"
                    on:click={activatePrivateKey}
                  >
                    unvest
                  </button>
                </div>
              </div>
            {/each}
          {/if}
        {/if}
      </div>
    </div>
  </div>
</div>
