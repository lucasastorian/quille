import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Message } from '../../../../../services/message/message.service';

@Component({
  selector: 'web-search-results',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './web-search-results.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class WebSearchResultsComponent {

  @Input() message: Message | undefined;

  public limit: 3 | 100 = 3;

}
