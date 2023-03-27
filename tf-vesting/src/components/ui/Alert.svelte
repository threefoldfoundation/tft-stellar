<script lang="ts">
  export let className: string;
  export let title: string | null = null;
  export let message: string;
  export let isOpen: boolean;
</script>

{#if isOpen}
  <div class="alert alert-{className}">
    {#if title}
      <h6 class="alert-heading text-capitalize">{title}</h6>
    {/if}
    {message}
  </div>
{/if}
