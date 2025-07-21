import type { DialogApiInjection } from 'naive-ui/es/dialog/src/DialogProvider';
import type { MessageApiInjection } from 'naive-ui/es/message/src/MessageProvider';

interface NaiveUiType {
  message: MessageApiInjection;
  dialog: DialogApiInjection;
}
const naiveui: NaiveUiType = {
  dialog: window?.$gm?.dialog,
  message: window?.$gm?.message,
};

export default naiveui;
