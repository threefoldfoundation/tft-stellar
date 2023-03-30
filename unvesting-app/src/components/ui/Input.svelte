<script lang="ts">
  import type { InputValidationsType } from '../../utils/types';

  export let value: string | undefined = undefined;
  export let label = '';
  export let type = 'text';
  export let disabled = false;
  export let className = '';
  export let validation: CallableFunction | undefined = undefined;
  export let onKeyPress: CallableFunction | undefined = undefined;
  export let isLoading: boolean;
  export let placeholder = '';

  let validateClass: string;
  const elmID: string = label.replace(/\s+/g, '-').toLowerCase();
  +'-id';
  let validated: InputValidationsType;

  function typeAction(node: HTMLInputElement) {
    node.type = type;
  }

  const _onKeyPress = (e: { keyCode: number }) => {
    onKeyPress(e);
  };

  const validate = () => {
    if (validation != undefined) {
      validated = validation(value);
      if (validated && validated.isValid) {
        validateClass = 'is-valid text-success';
      } else if (value === undefined) {
        validateClass = '';
      } else if (validated.isValid === false) {
        validateClass = 'is-invalid error-border text-danger';
      }
    }
  };

  $: value, validate();
</script>

<div class="form-group h-100 p-2 mb-2 w-100 d-contents p-relative">
  {#if label}
    <strong>
      <label for={elmID}>{label}</label>
    </strong>
  {/if}
  <input
    bind:value
    use:typeAction
    {disabled}
    class="form-control input {className} {validateClass}"
    style={type === 'password' ? 'display: inline;' : ''}
    id={elmID}
    on:keypress={_onKeyPress}
    {placeholder}
  />
  {#if isLoading}
    <div class="spinner-border input-spinner" role="status" />
  {/if}
  {#if type === 'password' && !isLoading}
    <!-- Eye icon to show password -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <i
      class="fa-solid fa-eye fa-eye-custom"
      id="eye"
      on:click={() => {
        const passwordInput = document.querySelector(`#${elmID}`);
        const type =
          passwordInput.getAttribute('type') === 'password'
            ? 'text'
            : 'password';
        passwordInput.setAttribute('type', type);
      }}
    />
  {/if}

  {#if validation != undefined && validated && validated.errorMessage}
    <div id={elmID} class="invalid-feedback">
      <span class="alert-link">{validated.errorMessage}</span>
    </div>
  {/if}
</div>

<svelte:head>
  <style>
    .input:focus {
      transition: all 0.1s linear;
      border: 0.5px solid rgb(255 0 30);
    }
    .error-validation {
      transition: all 0.1s linear;
      box-shadow: none;
      border: 1px solid rgb(255 0 30);
    }
    .success-validation {
      transition: all 0.1s linear;
      box-shadow: none;
      border: 1px solid rgb(255 0 30);
    }
    .form-control.is-invalid:focus,
    .was-validated .form-control:invalid:focus {
      box-shadow: none;
      border-color: rgb(249 49 84) !important;
    }
    .form-control.is-valid:focus,
    .was-validated .form-control:valid:focus {
      box-shadow: none;
      border-color: rgb(0 183 74) !important;
    }
    .fa-eye-custom {
      cursor: pointer;
      color: var(--text-primary);
      position: absolute;
      right: 15px;
      top: 43px;
      font-size: 17px;
      color: #3f72b6;
    }
    .invalid-feedback {
      width: auto;
      color: #f93154;
      margin-top: 0.25rem;
      right: 13px;
    }
    .form-control.is-invalid,
    .was-validated .form-control:invalid {
      margin-bottom: 0rem;
    }
    .form-control.is-valid,
    .was-validated .form-control:valid {
      margin-bottom: 0rem;
    }
  </style>
</svelte:head>
