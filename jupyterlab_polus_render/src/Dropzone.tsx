
import { Drag } from '@lumino/dragdrop';
import React, { useCallback, useEffect, useRef } from 'react';

declare global {
  // eslint-disable-next-line @typescript-eslint/interface-name-prefix
  interface HTMLElementEventMap {
    'lm-drop': Drag.Event;
  }
}

interface IRootProps {
  ref: React.RefObject<HTMLDivElement>;
}

interface IProps {
  children?: React.ReactNode; // Add children property
  onDrop?: (e: Drag.Event) => any;
}

interface IReturn {
  getRootProps: () => IRootProps;
}

export const useDropzone = (props: IProps): IReturn => {
  const rootRef = useRef<HTMLDivElement>(null);

  // const handleEvent = useCallback(
  //   (e: Drag.Event): void => {
  //     e.preventDefault();
  //     e.stopPropagation();
  //     switch (e.type) {
  //       case 'lm-drop':
  //         props.onDrop?.(e);
  //         break;
  //     }
  //   },
  //   [props]
  // );

  const handleEvent = useCallback(
    (e: Drag.Event): void => {
      e.preventDefault();
      e.stopPropagation();
      props.onDrop?.(e);
    },
    [props]
  );

  useEffect(() => {
    const node = rootRef.current;
    node?.addEventListener('lm-drop', handleEvent);

    return (): void => {
      node?.removeEventListener('lm-drop', handleEvent);
    };
  }, [handleEvent]);

  return {
    getRootProps: (): IRootProps => ({
      ref: rootRef
    })
  };
};

export const Dropzone: React.FC<IProps> = ({ children, ...rest }) => {
  const { getRootProps } = useDropzone(rest);

  return (
    <div style={{ height: '100%' }} {...getRootProps()}>
      {children}
    </div>
  );
};
