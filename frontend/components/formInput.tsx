import styles from "./formInput.module.css";

const FormInput = (props: {
  inputType: string;
  inputName: string;
  inputLabel: string;
}) => {
  return (
    <div className={styles.formInput}>
      <input type={props.inputType} placeholder=" " name={props.inputName} />
      <label htmlFor={props.inputName}>{props.inputLabel}</label>
    </div>
  );
};

export default FormInput;
