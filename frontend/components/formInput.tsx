import styles from "./formInput.module.css";
import { ChangeEventHandler, HTMLInputTypeAttribute } from "react";

const FormInput = (props: {
  inputType: HTMLInputTypeAttribute;
  inputName: string;
  inputLabel: string;
  errorMsg: string;
  changeHandler?: ChangeEventHandler;
}) => {
  return (
    <div className={styles.formInput}>
      <input
        type={props.inputType}
        placeholder=" "
        name={props.inputName}
        onChange={props.changeHandler}
        required
      />
      <label htmlFor={props.inputName}>{props.inputLabel}</label>
      <span className={"text-sm text-red-600"}>{props.errorMsg}</span>
    </div>
  );
};

export default FormInput;
