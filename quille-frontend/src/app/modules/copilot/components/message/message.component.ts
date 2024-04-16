import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Message } from '../../../../services/message/message.service';

@Component({
  selector: 'message',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './message.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MessageComponent {

  @Input() message: Message | undefined;

}
