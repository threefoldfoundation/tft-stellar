<script lang="ts">
  import { activatePKStore } from '../../utils/stores';
  import type { OnResponseVestingAccounts } from '../../utils/types';

  export let vestingAccounts: OnResponseVestingAccounts;
  const activatePrivateKey = () => {
    activatePKStore.set({
      address: vestingAccounts.vesting_accounts[0].address,
      isSelected: true,
    });
  };
</script>

<section class="mt-5">
  {#if vestingAccounts && !vestingAccounts.Error}
    {#if vestingAccounts.vesting_accounts.length}
      <h4 class="mb-4">Linked Address</h4>
      <div class="row">
        {#each vestingAccounts.vesting_accounts as account}
          <div class="col-6">
            <div class="card">
              <div class="card-body">
                <p class="mb-4">{account.address}</p>
                <button class="use-btn" on:click={activatePrivateKey}
                  >Use This Address</button
                >
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  {/if}
</section>
